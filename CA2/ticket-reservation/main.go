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
	ID   int
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

type TicketService struct {
	events sync.Map
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
	//implement concurrency control here
	//...
	event, ok := ts.events.Load(eventID)
	if !ok {
		return nil, fmt.Errorf("event not found")
	}
	ev := event.(*Event)

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
		fmt.Printf("||||||||||||||||| Error: %s |||||||||||||||||\n", e.Error())
	}
}

func CommandHandler(commands []string, jobId *JobID, ticketService *TicketService, chErr chan error, chOutput chan string) {
	jobId.mutx.Lock()
	jobId.ID = jobId.ID + 1
	id := jobId.ID
	jobId.mutx.Unlock()
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
	var jobId JobID
	jobId.ID = 0
	chOutput := make(chan string)
	chErr := make(chan error)

	go OutputManager(chOutput)
	go ErrorManager(chErr)
	for true {
		inputCommand, _ := reader.ReadString('\n')
		commands := strings.Split(strings.TrimSpace(strings.ToLower(inputCommand)), " ")

		if commands[0] == "exit" {
			break
		} else if commands[0] == "help" {
			fmt.Println(HELP_MESSAGE)
		} else if strings.Contains(COMMANDS, commands[0]) {
			go CommandHandler(commands, &jobId, ticketService, chErr, chOutput)
		} else {
			chErr <- fmt.Errorf("Erro: command not found")
		}
	}

	close(chOutput)
	close(chErr)

}
