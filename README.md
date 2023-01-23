# zse_diportal

You must first log in to the website manually. Run inspect element, for example, in the Google Chrome browser. Watch the "getProfileData" POST request's. 
Click on "Odberné miesta", then on "Int. dáta" in the menu. There you will find all your necessary data (getProfileData's payload).

Cookies must be saved in the cookie.txt file. Cookie text file must contain parameters: JSESSIONID, JSESSIONMARKID, TS5dXXXXXXXXX (It might be unique, so I left it out).
The session expires from time to time, so you have to log in again manually and save the cookie in the cookie.txt file.

I recommend running the script with contab as often as possible so that the session does not expire.

Tested:<b>
usage: python3.9 [option] ... [-c cmd | -m mod | file | -] [arg] ...<br>
Try `python -h' for more information.
</b>
