# DeckDazzle

DeckDazzle uses OpenAI GPT-4-Turbo and DALL-E to create a PowerPoint deck from a single keyword.

We made this to use in PowerPoint Karaoke settings, but can maybe be useful in other settings as well.

This is a work in progress, there's a lot to figure out, and we welcome contributions of any kind. Simply fork us and open PRs.

## API Key

**Do not** push the file apikeys.py if it contains the OpenAI API key. The apikeys.py file has been added to the _.gitignore_.

If an OpenAI API key has been inadvertently pushed to the repository and is publicly accessible, please remove it from both the file **and** from OpenAI. Then, generate a new OpenAI API key.

# How to use

**This does not work on Windows. If you have a Windows machine, you need to use WSL. On some macOS and Linux versions, the command required the use of _python3_ and not _python_**

Create a folder named _presentations_ in the root of the repo. Add your OpenAI key and organization (which can be found under _Settings_ on the OpenAI login page) to the _apikeys.py_ file.

Install all the required packages by typing

```
python -m pip install -r requirements.txt
```

Then, you can run the flask server by typing

```
python server.py
```

Go to the website, and type the name of the PowerPoint that you want to generate. **Remember**, that OpenAI have some _Safety_ requirements and something that is considered to vulgar for the API will not be generated.
There is no guideline for this, and the best way to figure out the limit is to experiment.

When the PowerPoint has been generated, you can download it by pressing the presentation link.

## Todo list

- [x] Create a basic HTML home page with 1) prompt to create new presos and 2) a list of existing presos for download
- [x] Style this thing to make it look like something
- [ ] Secure all inputs to the API. It is DANGEROUS to make this version publicly available. 
- [ ] Handle errors in generation and replace infinite loops
- [ ] Support multiple languages?
- [ ] Improvements of any kind - we're open to anything so send those PRs!
- [ ] Setup for azure hosting (see https://learn.microsoft.com/en-us/azure/container-apps/background-processing?tabs=bash)
