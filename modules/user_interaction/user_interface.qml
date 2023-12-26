import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 6.6

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "CIARAN"
    
    FileDialog {
        id: fileDialog
        title: "Select a File"
        nameFilters: ["Text files (*.txt)", "All files (*)"]
        onAccepted: {
            if (fileDialog.fileUrls.length > 0) {
                // Pass the selected file path to Python backend for processing
                backend.processFile(fileDialog.fileUrls[0])
            }
        }
    }

    Button {
        text: "Upload File"
        onClicked: fileDialog.open()
    }
}