grouptweetbot
=============

A small python script to read an account's timeline and retweet some tweets under the following conditions:

  * The tweet starts with "@botaccount": In this case "@botaccount" will be replaced with "RT @sender: " 
    in the resulting tweet (there's a configurable rate limit per sender).
  * The tweet is a Direct Message from an account the Bot account follows: The bot just retweets it as 
    if the bot itself wrote the message (w/o rate limit).

To work with this bot, you'll need to get some tokens from https://dev.twitter.com. These tokens have to 
be put into the script.

