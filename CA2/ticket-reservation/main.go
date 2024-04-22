package main

import (
	"fmt"
	"time"
)

type Event struct {
	ID					string
	Name				string
	Data				time.Time
	TotalTickets		int
	AvailableTickets 	int
}

type Ticket struct {
	ID 		string
	EventID string
}

func main() {
	fmt.Println("Hello world")
}