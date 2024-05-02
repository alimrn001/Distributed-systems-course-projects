package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"ticket-reservation/utils"
	"time"
)

const DATE_LAYOUT = "2006-01-02_15:04:05"

const COMMANDS = "help,exit,create,book,list"

const TOTAL_NUM_OF_PROCESS = 3

const NUM_CACHE = 3

const HELP_MESSAGE = `
Commands are:
	* create new event:
		- create <name: str> <date: 2006-01-02_15:04:05> <numTickets: int>
	* book tickets:
		- book <eventId: str> <numTickets: int>
	* listing events:
		- list
	* help menue:
		- help 
	* exiting the program:
		- exit`

type JobID struct {
	mutx sync.Mutex
}

type Event struct {
	ID               string
	Name             string
	Date             time.Time
	TotalTickets     int
	AvailableTickets int
	mutx             sync.Mutex // Mutex for synchronizing access to AvailableTickets
}

type Ticket struct {
	ID      string
	EventID string
}

type Cache struct {
	accessCount sync.Map
	events      [NUM_CACHE]*Event
	// mutxs           [NUM_CACHE]sync.Mutex
	accessCountMutx sync.Mutex
}

type TicketService struct {
	cache  Cache
	events sync.Map
}

type ProcessManager struct {
	ID                int
	numProcessRunning int
	mutx              sync.Mutex
	wg                sync.WaitGroup
}

func NewTicketService() *TicketService {
	return &TicketService{}
}

func (ts *TicketService) CreateEvent(name string, date time.Time, totalTickets int) (*Event, error) {
	event := &Event{
		ID:               utils.GenerateUUID(),
		Name:             name,
		Date:             date,
		TotalTickets:     totalTickets,
		AvailableTickets: totalTickets,
	}

	ts.events.Store(event.ID, event)
	return event, nil
}

func (ts *TicketService) ListEvents() []*Event {
	var events []*Event
	ts.events.Range(func(key, value interface{}) bool {
		event := value.(*Event)
		events = append(events, event)
		return true
	})
	return events
}

func (ts *TicketService) BookTickets(eventID string, numTickets int) ([]string, error) {

	// use cache or access main database
	var event any
	var ok bool
	event, ok = ts.cache.FindEvent(eventID)
	if !ok {
		event, ok = ts.events.Load(eventID)
		if !ok {
			return nil, fmt.Errorf("event not found")
		}
	}

	ev := event.(*Event)
	ts.cache.AddAccessCountAndUpdateCache(eventID, ev)

	ev.mutx.Lock()
	defer ev.mutx.Unlock()
	if ev.AvailableTickets < numTickets { //critical section
		return nil, fmt.Errorf("not enough tickets available")
	}

	var ticketIDs []string
	for i := 0; i < numTickets; i++ {
		ticketID := utils.GenerateUUID()
		ticketIDs = append(ticketIDs, ticketID)
		//store the ticket in a seperate data structure if needed
	}

	ev.AvailableTickets -= numTickets
	ts.events.Store(eventID, ev)

	return ticketIDs, nil
}

func (ts *TicketService) PrintListEvents(chOutput chan string) {
	events := ts.ListEvents()
	chOutput <- fmt.Sprint("Events:")
	for _, event := range events {
		chOutput <- fmt.Sprintf("ID: %s, Name: %s, Date: %s, Total Tickets: %d, Available Tickets: %d\n", event.ID, event.Name, event.Date.String(), event.TotalTickets, event.AvailableTickets)
	}
}

func (cache *Cache) AddAccessCountAndUpdateCache(eventId string, event *Event) {
	count, ok := cache.accessCount.Load(eventId)
	if !ok {
		cache.accessCount.Store(eventId, 1)

	} else {
		cache.accessCount.Store(eventId, count.(int)+1)
	}

	// update accessCount
	cache.accessCountMutx.Lock()
	defer cache.accessCountMutx.Unlock()
	for i, ev := range cache.events {
		if ev == nil {
			cache.events[i] = event
			break
		}
		if ev == event {
			if i == 0 {
				break
			}
			higherAccess, _ := cache.accessCount.Load(cache.events[i-1].ID)
			lowerAccess, _ := cache.accessCount.Load(event.ID)
			if lowerAccess.(int) > higherAccess.(int) { // swap
				cache.events[i] = cache.events[i-1]
				cache.events[i-1] = event
			}
			break
		}
		if i == len(cache.events)-1 { // last element
			higherAccess, _ := cache.accessCount.Load(ev.ID)
			lowerAccess, _ := cache.accessCount.Load(event.ID)

			if lowerAccess.(int) > higherAccess.(int) { // replace
				cache.events[i] = event
			}
		}
	}
}

func (cache *Cache) FindEvent(eventId string) (*Event, bool) {
	for _, ev := range cache.events {
		if ev == nil {
			return nil, false
		}
		if ev.ID == eventId {
			return ev, true
		}
	}
	return nil, false
}

func CreateTicketCommand(jobId int, ts *TicketService, commands []string, chErr chan error, chOutput chan string) {
	if len(commands) != 4 {
		chErr <- fmt.Errorf("wrong format(use help command)")
		return
	}

	name := commands[1]
	date, err := time.Parse(DATE_LAYOUT, commands[2])
	if err != nil {
		chErr <- err
		return
	}
	numTicket, err := strconv.Atoi(commands[3])
	if err != nil {
		chErr <- err
		return
	}
	if _, err := ts.CreateEvent(name, date, numTicket); err != nil {
		chErr <- err
		return
	}

	chOutput <- fmt.Sprintf("CreateTicket with id %d has been done!", jobId)
}

func BookTicketsCommand(jobId int, ts *TicketService, commands []string, chErr chan error, chOutput chan string) {
	if len(commands) != 3 {
		chErr <- fmt.Errorf("wrong format(use help command)")
		return
	}

	id := commands[1]

	numTickets, err := strconv.Atoi(commands[2])
	if err != nil {
		chErr <- err
		return
	}

	if _, err := ts.BookTickets(id, numTickets); err != nil {
		chErr <- err
		return
	}

	chOutput <- fmt.Sprintf("BookTicket with id %d has been done!", jobId)

}

func OutputManager(ch <-chan string) {
	for v := range ch {
		fmt.Println(v)
	}
}

func ErrorManager(ch <-chan error) {
	for e := range ch {
		fmt.Printf("**** Error: %s ****\n", e.Error())
	}
}

func CommandHandler(commands []string, processManager *ProcessManager, ticketService *TicketService, chErr chan error, chOutput chan string) {

	processManager.mutx.Lock()
	processManager.ID++
	processManager.numProcessRunning++
	id := processManager.ID
	processManager.mutx.Unlock()
	defer processManager.wg.Done()

	chOutput <- fmt.Sprintf("Your request with id %d is processing ... \n", id)

	switch commands[0] {
	case "create":
		CreateTicketCommand(id, ticketService, commands, chErr, chOutput)

	case "book":
		BookTicketsCommand(id, ticketService, commands, chErr, chOutput)

	case "list":
		ticketService.PrintListEvents(chOutput)
	}
}

func main() {

	// initialize
	ticketService := NewTicketService()
	ticketService.CreateEvent("Concert", time.Now(), 100)
	ticketService.CreateEvent("Conference", time.Now(), 200)

	reader := bufio.NewReader(os.Stdin)
	var processManager ProcessManager
	chOutput := make(chan string)
	chErr := make(chan error)

	go OutputManager(chOutput)
	go ErrorManager(chErr)
	for {
		if processManager.numProcessRunning >= TOTAL_NUM_OF_PROCESS {
			fmt.Printf("Error: maximum request reached. wait ...\n")
			processManager.wg.Wait()
		}

		inputCommand, _ := reader.ReadString('\n')
		commands := strings.Split(strings.TrimSpace(strings.ToLower(inputCommand)), " ")

		if commands[0] == "exit" {
			break
		} else if commands[0] == "help" {
			fmt.Println(HELP_MESSAGE)
		} else if strings.Contains(COMMANDS, commands[0]) {
			processManager.wg.Add(1)
			go CommandHandler(commands, &processManager, ticketService, chErr, chOutput)
		} else {
			chErr <- fmt.Errorf("Erro: command not found")
		}

	}

	close(chOutput)
	close(chErr)
}
