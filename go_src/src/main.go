package main

import (
    "fmt"
    "github.com/docopt/docopt-go"
)

var usage = `usage: sorter [-i <input data file>] [-o <output sorted data file>] [-a <the sort algorithm>]
options:
    -h     Show this screen
    -i     Set input file name
    -o     Set output file name
    -a     Set sorting algorithm
`

var banner string = `
   ______    ___
  / ____/   (* *)
 (___  )   (  0  )
/_____/   (  ___  )
`
var (
    infile string = "indata"
    outfile string = "outdata"
    algorithm string = "qsort"
)

func main() {
    fmt.Print(banner)
    args, err := docopt.Parse(usage, nil, true, "sorter 0.1", true)
    if err != nil {
        fmt.Println(err)
    }

    if args["-i"] != nil {
        infile = args["-i"].(string)
    }

    if args["-o"] != nil {
        outfile = args["-o"].(string)
    }

    if args["-a"] != nil {
        algorithm = args["-a"].(string)
    }

    fmt.Print("infile=", infile, "outfile=", outfile, "algorithm=", algorithm)

}
