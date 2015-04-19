package algorithm

type Sorter interface {
    BubbuleSort(seq []interface{}) (out []interface{}, err error)
    InsertSort(seq []interface{}) (out []interface{}, err error)
    SelectSort(seq []interface{}) (out []interface{}, err error)
    QSort(seq []interface{}, low, high int) (out []interface{}, err error)
    MergeSort(seq []interface{}, low, high int) (out []interface{}, err error)
    HeapSort(seq []interface{}, low, high int) (out []interface{}, err error)
}

type GoSorter struct {
    name string
    cycle int
    count int
    verbose bool 
} 
