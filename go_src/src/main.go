package main

import (
    "fmt"
    "flag"
    "os"
    "algorithm"
)

var usage = `usage: sorter [-i <input data file>] [-o <output sorted data file>] [-a <the sort algorithm>]
options:
    -h     Show this screen
    -i     Set input file name
    -o     Set output file name
    -a     Set sorting algorithm
`

var banner string = `

||\\  ||     A     ||        A
|| \\ ||   //_\\   ||      //_\\
||  \\||  //   \\  ||___  //   \\
`

var (
    infile = flag.String("i", "indata", "")
    outfile = flag.String("o", "outdata", "")
    algorithms = flag.String("a", "qsort", "")
)

func main() {
    fmt.Print(banner)
    flag.Usage = func() {
        fmt.Fprint(os.Stderr, "\n\n")
        fmt.Fprint(os.Stderr, fmt.Sprintf(usage))
    }

    flag.Parse()

    var s algorithm.Sorter = &algorithm.GoSorter{
        Name : "anan",
        Cycle : 0,
        Count : 0,
        Verbose : false,
    }

    seq := []int{3,2,1,0, -1, 5, 0, 2} // test
    var err error
    seq, err = s.BubbleSort(seq)
    seq, err = s.InsertSort(seq)
    if err != nil {
        fmt.Println(err)
    } else {
        fmt.Println(seq)
    }

}

func showUsageAndExit(msg string) {
    if msg != "" {
        fmt.Fprint(os.Stderr, msg)
        fmt.Fprint(os.Stderr, "\n\n")
    }
    flag.Usage()
    fmt.Fprint(os.Stderr, "\n")
    os.Exit(1)
}
