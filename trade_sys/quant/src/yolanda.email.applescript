on run {mailSubject, mailContent}
    tell application "Mail"
        set my_message to make new outgoing message
        set subject of my_message to mailSubject
        set content of my_message to mailContent
        set sender of my_message to "yolanda.cheung.1997@gmail.com"

        --
        tell my_message
            make new to recipient at end of to recipients with properties {name:"yolanda.cheung.1997@gmail.com"}
        end tell
        --

        send my_message
    end tell
end run

