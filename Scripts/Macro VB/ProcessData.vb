Sub ProcessData()
    Dim inputData As String
    Dim dataArray() As String
    Dim resultsArray(5) As String
    Dim startCell As Range
    Dim i As Integer

    ' Prompt the user for the input data line
    inputData = InputBox("Enter the data line:", "Data Input")

    ' Check if the user provided any input
    If inputData = "" Then
        MsgBox "No data provided. Exiting.", vbExclamation
        Exit Sub
    End If

    ' Split the input data by spaces and tabs
    dataArray = Split(inputData, vbTab)

    ' Ensure there are enough elements in the data array
    If UBound(dataArray) < 5 Then
        MsgBox "Invalid data provided. Please ensure the data line has at least 6 elements.", vbCritical
        Exit Sub
    End If

    ' Assuming the first element is the text we want to remove, and the rest are numbers
    For i = 1 To 5
        resultsArray(i - 1) = dataArray(i)
    Next i
    resultsArray(5) = "" ' Time (s) left blank

    ' Set the starting cell to the currently selected cell
    Set startCell = Selection

    startCell.Offset(0, 0).Value = resultsArray(0)
    startCell.Offset(1, 0).Value = resultsArray(1)
    startCell.Offset(2, 0).Value = resultsArray(2)
    startCell.Offset(3, 0).Value = resultsArray(3)
    startCell.Offset(4, 0).Value = resultsArray(4)
    startCell.Offset(5, 0).Value = resultsArray(5)

End Sub
