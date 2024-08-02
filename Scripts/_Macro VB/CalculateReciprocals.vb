Sub CalculateReciprocals()
    Dim cell As Range
    Dim result As Variant
    
    ' Loop through each cell in the selected range
    For Each cell In Selection
        ' Check if the cell contains a numeric value
        If IsNumeric(cell.Value) Then
            ' Calculate the reciprocal
            result = 1 / cell.Value
            result=round(result,2)
            
            ' Place the result in the cell next to the current cell
            cell.Offset(0, 1).Value = result
        Else
            ' If the cell does not contain a numeric value, output an error message in the next cell
            cell.Offset(0, 1).Value = "Invalid Input"
        End If
    Next cell
End Sub
