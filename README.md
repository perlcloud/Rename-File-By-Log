# Rename Files by Log
###### Log the subject you are currently photographing. Use the log later to rename all photos taken with the corresponding subject ID
This tool was built with high volume photographers in mind who need to have their files renamed to have the subject id as the filename.

## Logging Subject Timing 
###### Run the `Subject-Logger.py` script

Enter the name of your project when prompted.
```
Enter the job name: My test project
```
Your project name will be standardized to work as a filename and you will be prompted to confirm
```
Your job will be saved as "My_test_project" ok? (Y/N):
```
Enter `Y` for "yes" or `N` for "no".

You have now started your project and are ready to enter your first subject id.

_Tip: use a barcode scanner to scan the code on your project or pre-printed subject cards! Make sure the scanner is set to send `return` after each scan._
```
---------- My_test_project ----------
Current ID:
```
When you enter your ID, the start time will be logged in a .csv file created in the project root folder with your project name. You are immediately prompted for the next subject when ready.

_Note: If your subject id is incompatible with windows file name rules, your subject ID will be standardized with the new version displayed._
```text
---------- My_test_project ----------
Current ID: Subject 1
Current ID (cleaned): Subject_1
Timestamp: 2019-02-22 01:48:42.633842
-------------------------------------
Current ID:
```
When ready, enter your next subject ID. The start time of a subject card is the end time of the previous.

#### Ending Log
When you are done working on your last subject, enter `end` as your subject id and the job will be ended.

## Renaming subject files
Run the `File-Rename.py` script

Enter the name of your project
```text
Enter the job name: My test job
```
The script will than try to locate the relevant .csv file, expecting a file named `./My_test_project.csv`.

The script will than rename each file in your project folder according to the subject id listed in the .csv file. For your records, a log of name changes is created.

## Problems
The script assumes that your computers clock is synced perfectly with your camera. This is never the reality. To deal with this, I am working on a tool that will help you calculate the offset between devices. The offset will be entered into the renaming program and it will use that to get the timing correct.

This is not done, but the basic workflow will be to run `Offset-Clock.py` which will display the current computer time. With your camera you photograph the clock. Once you've loaded the photo onto your computer you can run `Offset-Calculator.py` which will ask you for the path to the photo.

The script will than calculate the offset which you will enter into the renaming script.

## Todo

-[ ] Find a way to deal with jpg+raw to keep the same name
-[ ] Add error handling 
-[ ] Offset calculation 