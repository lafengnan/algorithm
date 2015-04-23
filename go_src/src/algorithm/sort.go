package algorithm

type Sorter interface {
    BubbleSort(seq []int) (out []int, err error)
    InsertSort(seq []int) (out []int, err error)
    /*
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

func (s *GoSorter) InsertSort(seq []int) (out []int, err error) {
    out = seq
    var i, j int
    for i = 1; i < len(seq); i++ {
        key := seq[i]
        for j = i - 1; j >= 0; j-- {
            if key <= seq[j]{
                seq[j+1] = seq[j]
            } else {
                break
            }
        }
        seq[j+1] = key
    }
    return
}
