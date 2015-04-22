package algorithm

type Sorter interface {
    BubbleSort(seq []int) (out []int, err error)
    /*
    InsertSort(seq []int) (out []int, err error)
    SelectSort(seq []int) (out []int, err error)
    QSort(seq []int, low, high int) (out []int, err error)
    MergeSort(seq []int, low, high int) (out []int, err error)
    HeapSort(seq []int, low, high int) (out []int, err error)
    */
}

type GoSorter struct {
    Name string
    Cycle int
    Count int
    Verbose bool 
} 

func (s *GoSorter) BubbleSort(seq []int) (out []int, err error) {
    out = seq
    for j := len(seq) - 1; j > 0; j-- {
        for i := 0; i < j; i++ {
            if seq[i] > seq[i+1] {
                seq[i], seq[i+1] = seq[i+1], seq[i]
            }
        }
    }
    return 
}
