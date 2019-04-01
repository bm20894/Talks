package main

import (
	"fmt"
)

// show A type
type A struct {
	name string
}

// end A type OMIT

func main() {
	fmt.Println("Hello, World!")
}

func printStr(s string) { // HLone
	fmt.Println(s) // HL
}
