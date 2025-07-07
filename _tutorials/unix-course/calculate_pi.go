package main

import (
	"fmt"
	"time"
)

func main() {
	var pi float64 = 0.0
	for i := 1.0; i <= 1e12; i += 4.0 {
		pi += 4.0 / i
		pi -= 4.0 / (i + 2.0)
		if int(i)%1e9 == 1 || i < 30 {
			fmt.Printf("Approximation after %12d steps: %.26f\n", int(i), pi)
		}
		if i < 30 {
			time.Sleep(1 * time.Second)
		}
	}
}
