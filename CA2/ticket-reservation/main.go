package main

import (
	"fmt"
	"time"
	"ticket-reservation/utils"
	"sync"
)

type Event struct {
	ID					string
	Name				string
	Date				time.Time
	TotalTickets		int
	AvailableTickets 	int
	mutx				sync.Mutex // Mutex for synchronizing access to AvailableTickets
}

type Ticket struct {
	ID 		string
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


func main() {
	ticketService := NewTicketService()

	// Creating new events
	ticketService.CreateEvent("Concert", time.Now(), 100)
	ticketService.CreateEvent("Conference", time.Now(), 200)

	// Listing events
	events := ticketService.ListEvents()
	fmt.Println("Events:")
	for _, event := range events {
		fmt.Printf("ID: %s, Name: %s, Date: %s, Total Tickets: %d, Available Tickets: %d\n", event.ID, event.Name, event.Date.String(), event.TotalTickets, event.AvailableTickets)
	}
}
