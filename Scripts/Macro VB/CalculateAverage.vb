Sub CalculateAverage()
    Dim value1 As Double
    Dim value2 As Double
    Dim value3 As Double
    Dim average As Double
    Dim startCell As Range

    ' Prompt the user to enter three values
    value1 = InputBox("Enter the first value:", "Input Value 1")
    value2 = InputBox("Enter the second value:", "Input Value 2")
    value3 = InputBox("Enter the third value:", "Input Value 3")

    ' Calculate the average of the three values
    average = (value1 + value2 + value3) / 3

    ' Round the average to the nearest 1 decimal place
    average = WorksheetFunction.Round(average, 1)

    ' Set the starting cell to the currently selected cell
    Set startCell = Selection

    ' Output the rounded average to the selected cell
    startCell.Value = average

    MsgBox "The average of the three values (rounded to 1 decimal place) is: " & average
End Sub
