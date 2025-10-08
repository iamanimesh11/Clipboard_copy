Dim sb As New System.Text.StringBuilder()

' Start table with class
sb.append(title)
sb.Append("<table class='custom-table'>")
Dim colindex As Integer=0
' Add table headers with conditional formatting
Dim headerClassMap As New Dictionary(Of String, String)() ' Stores the header class for each column by name

sb.Append("<tr class='header-row'>")
For Each col As System.Data.DataColumn In dtData.Columns
    Dim headerText As String = col.ColumnName
    Dim headerClass As String = ""
    Dim headerTextLower As String = headerText.ToLower() ' Convert to lowercase once for efficiency
	If colindex =2 Then
		headerText="Total"
	End If


    sb.Append("<th class='" & headerClass & " header-centre'>" & headerText & "</th>")

    ' Store the header class for this column
    headerClassMap.Add(headerText, headerClass)
	colindex+=1
Next
sb.Append("</tr>")

' Add table rows with alternating colors and conditional formatting for Status
Dim rowIndex As Integer = 0

For Each row As DataRow In dtData.Rows
	If row(0).TOstring().ToLower().contains("total") Or row(0).TOstring().ToLower().contains("blank") Then 
		If row(0).TOstring().ToLower().contains("grand") Then
		Else 
		Continue For
	End If
	End If
    Dim rowClass As String = If(rowIndex Mod 2 = 0, "even-row", "odd-row")
    sb.Append("<tr class='" & rowClass & "'>")

    For Each col As System.Data.DataColumn In dtData.Columns
    Dim cellValue As String = row(col.ColumnName).ToString()
    Dim cellClass As String = ""
 

 If rowIndex=dtDATA.Rows.Count -1 Then 
		cellClass &= " bold_txt"
		
	End If 

	
    ' Center-align numeric values
    If IsNumeric(cellValue)Then
        cellClass &= " cell-center"
	  If CInt(cellValue)<0 Then 
		cellClass &=" lessthan0"
	End If 
    End If


    sb.Append("<td class='" & cellClass.Trim() & "'>" & cellValue & "</td>")
Next

    sb.Append("</tr>")
    rowIndex += 1
Next

sb.Append("</table>")
htmlTable = sb.ToString()
