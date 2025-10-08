Dim sb As New System.Text.StringBuilder()

' Start table with class
sb.Append(title)
sb.Append("<table class='custom-table'>")

' Add table headers
Dim colIndex As Integer = 0
Dim headerClassMap As New Dictionary(Of String, String)() ' Stores the header class for each column by name

sb.Append("<tr class='header-row'>")
For Each col As System.Data.DataColumn In dtData.Columns
    Dim headerText As String = col.ColumnName
    Dim headerClass As String = ""

    ' Rename the 3rd column (index 2) to "Total"
    If colIndex = 2 Then
        headerText = "Total"
    End If

    sb.Append("<th class='" & headerClass & " header-centre'>" & headerText & "</th>")

    ' Store the header class
    headerClassMap.Add(headerText, headerClass)
    colIndex += 1
Next
sb.Append("</tr>")

' Add table rows with alternating colors
Dim rowIndex As Integer = 0
For Each row As DataRow In dtData.Rows
    ' Skip certain rows unless they contain "grand"
    If row(0).ToString().ToLower().Contains("total") Or row(0).ToString().ToLower().Contains("blank") Then
        If Not row(0).ToString().ToLower().Contains("grand") Then
            Continue For
        End If
    End If

    Dim rowClass As String = If(rowIndex Mod 2 = 0, "even-row", "odd-row")
    sb.Append("<tr class='" & rowClass & "'>")

    For Each col As System.Data.DataColumn In dtData.Columns
        Dim cellValue As String = row(col.ColumnName).ToString()
        Dim cellClass As String = ""

        ' Bold the last row
        If rowIndex = dtData.Rows.Count - 1 Then
            cellClass &= " bold_txt"
        End If

        ' Format numeric values
        If IsNumeric(cellValue) Then
            cellClass &= " cell-center"

            ' Special formatting for "Total" column
            If col.ColumnName.ToLower() = "total" Or (colIndex = 2) Then
                Dim numberValue As Decimal = Convert.ToDecimal(cellValue)
                cellValue = numberValue.ToString("#,##0.00") ' Comma-separated, 2 decimal places
            End If

            ' Highlight negative numbers
            If Convert.ToDecimal(cellValue) < 0 Then
                cellClass &= " lessthan0"
            End If
        End If

        sb.Append("<td class='" & cellClass.Trim() & "'>" & cellValue & "</td>")
    Next

    sb.Append("</tr>")
    rowIndex += 1
Next

sb.Append("</table>")
htmlTable = sb.ToString()