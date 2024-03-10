on run
    tell application "Messages"
        set phoneNumber to "+8618684914209"
        set phoneNumber to "+8615574989048"
        set message to "比特币"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy phoneNumber of targetService
        send message to targetBuddy
    end tell
end run

