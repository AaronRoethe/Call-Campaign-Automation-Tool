set venv=offsite
call %USERPROFILE%\Anaconda3\Scripts\activate %USERPROFILE%\Anaconda3 
call activate base

call conda env create --file environment.yml
call activate %venv%
PAUSE