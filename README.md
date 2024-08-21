# DeckDazzle

DeckDazzle uses OpenAI GPT-4 and DALL-E to create a PowerPoint deck from a single keyword.

We made this to use in PowerPoint Karaoke settings, providing a surprising and (hopefully) fun style of improv theater.

You can now [test this on DeckDazzle.no](https://deckdazzle.no).

This is a work in progress, there's a lot to figure out, and we welcome contributions of any kind. Simply fork us and open PRs.

## Todo list

- [x] Create a basic HTML home page with 1) prompt to create new presos and 2) a list of existing presos for download
- [x] Style this thing to make it look like something
- [ ] Secure all inputs to the API. It is DANGEROUS to make this version publicly available. 
- [ ] Handle errors in generation and replace infinite loops
- [ ] Support multiple languages?
- [ ] Improvements of any kind - we're open to anything so send those PRs!
- [ ] Setup for azure hosting (see https://learn.microsoft.com/en-us/azure/container-apps/background-processing?tabs=bash)
