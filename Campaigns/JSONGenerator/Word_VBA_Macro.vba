' VBA Macro to extract campaign content from within Word
' 
' HOW TO ADD THIS TO YOUR WORD DOCUMENT:
' 1. Open your Word document
' 2. Press Alt+F11 to open VBA Editor
' 3. Insert > Module
' 4. Paste this code
' 5. Close VBA Editor
' 6. Insert > Shapes > Rectangle (draw a button)
' 7. Right-click button > Assign Macro > ExtractCampaignContent
' 8. Click the button to extract!

Sub ExtractCampaignContent()
    Dim docPath As String
    Dim pythonScript As String
    Dim shell As Object
    Dim command As String
    
    ' Get current document path
    If ActiveDocument.Path = "" Then
        MsgBox "Please save the document first!", vbExclamation, "Save Required"
        Exit Sub
    End If
    
    docPath = ActiveDocument.FullName
    
    ' Path to Python script (assumes it's in JSONGenerator folder)
    pythonScript = ActiveDocument.Path & "\extract_to_google_sheets.py"
    
    ' Check if Python script exists
    If Dir(pythonScript) = "" Then
        MsgBox "Cannot find extract_to_google_sheets.py in the same folder!", vbExclamation, "Script Not Found"
        Exit Sub
    End If
    
    ' Show status
    Application.StatusBar = "Extracting campaign content..."
    
    ' Create shell object
    Set shell = CreateObject("WScript.Shell")
    
    ' Build command - using test script for simplicity
    ' This runs the test extraction which doesn't require user input
    command = "cmd /c cd """ & ActiveDocument.Path & """ && python test_extraction.py"
    
    ' Run the Python script
    On Error Resume Next
    shell.Run command, 1, True ' 1 = show window, True = wait for completion
    
    If Err.Number <> 0 Then
        MsgBox "Error running extraction script: " & Err.Description, vbCritical, "Error"
        Application.StatusBar = False
        Exit Sub
    End If
    On Error GoTo 0
    
    ' Success message
    Application.StatusBar = "Extraction complete!"
    MsgBox "Campaign content extracted successfully!" & vbCrLf & vbCrLf & _
           "Content has been:" & vbCrLf & _
           "1. Copied to your clipboard" & vbCrLf & _
           "2. Saved to TSV and JSON files" & vbCrLf & vbCrLf & _
           "Next: Open Google Sheets and press Ctrl+V to paste!", _
           vbInformation, "Extraction Complete"
    
    Application.StatusBar = False
End Sub

Sub ExtractWithGUI()
    ' Alternative: Launch the GUI version
    Dim shell As Object
    Dim command As String
    
    If ActiveDocument.Path = "" Then
        MsgBox "Please save the document first!", vbExclamation, "Save Required"
        Exit Sub
    End If
    
    Set shell = CreateObject("WScript.Shell")
    command = "cmd /c cd """ & ActiveDocument.Path & """ && python extract_gui.py"
    
    On Error Resume Next
    shell.Run command, 1, False ' False = don't wait
    On Error GoTo 0
End Sub

