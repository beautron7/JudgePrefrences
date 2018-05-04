# What is this?
this is a bunch of disconnected thoughs about the program

# What does the end program look like?
When the end user starts the program, they can:
1. type in their numerical preferences and click a button to get a pref sheet
2. select a few attributes and have the program  "highlight" sentences that are indicative of that attribute.
3. rate a couple of paradigms so that the network can learn what the user likes and take over

# What do you mean numerical preferences?
Each team's specific desires for a debate judge are comprised of a number of factors, including a judge's attitude to particular arguments, their experience both in judging and in the debate community, school affiliation, and tolerance of speed

Creating an accurate representation of exactly which "type" of judge a certain debater prefers would cause at least some psychological damage to us, so we approximate the result numerically. Essentially, for each category or attribute, we have a set number of categories (0,1,2..), each of which corresponds to a particular variant of that attribute. For example, a category like "views on reading Counterplans" could range from 0 (really hates counterplans) to 4 (can't go without them) or anywhere in between. 

This numerical representation allows a user to specify approximately which kind of judge they want by simply inputting which score they would like in each category. For example, if the categories are ("speed reading", "counterplans", "experience"), then a (4,0,2) judge indicates you want a judge who loves speed, hates counterplans, and has moderate experience. 


#How do we auto-find scores?
Yay! So we have our scores. What about matching those automatically to judge profiles?

A few steps:

First, the word Neural network:
  Our training data is every individual word in all judge parameters, along with the word right before and right after
  Input layer is the 4000 or so most common words. The Output Layer is supposed to be the words that appear in a similar context.
  Using one hidden layer of 300 nodes, we attempt to categorize each word into a particular "type," so that the output layer (of same dimension as the input layer) will give us words that relate strongly to the input word. This allows us to handle words with synonyms, such as "good" and "great" and "glorious" so that "I think K's are glorious" gives us the same result as "I think K's are great"
  The really useful part of this network is the hidden layer of 300, which allows us to distill any particular word into an array of 300 values. This then allows us to take any sentence of words and turn it into a 2d array of those arrays of 300 values, creating a sort of "map" which accurately reflects the "type" or "gist" of each word of that sentence. I'll call this a "wordmap"

Second, the sentence network:
  Our training data is a bunch of "snippets" of judge paradigms which have been converted into wordmaps, each snippet corresponding to a particular score for a particular category
  The network takes a wordmap as input and tries to categorize it into a specifc attribute and score. For example, the sentence "Counterplans are literally satan" just give us ("counterplan", 0) 
  In order to get this to work with judge paradigms that often have lengthy paragraphs, we limit the window of consideration of the neural network to only a few words long, and "dull" the value/weights of the words that are farther off

This entire process can be visualized as converting sentences to "images" which provide a broad overview of the "meaning" of the sentence regardless of the specific word used. It's a bit like having a person translate poems for you into plain english regardless of the fancy language originally being used. The image strips down words into their barebones meaning. After that, we just use image recognition to determine which category the image corresponds to, if any at all.
  
# What about teams that do \_\_\_\_\_? Why dont we also look for \_\_\_\_?
Each team has different things they look for in a judge. while many teams may want to look for simialr attributes, some teams may want to look for an attribute we didnt code in. Because of this, it would make sense to allow users to write thier own features. Here is a specification on 




The final network will take in a paragraph of text, convert it to a 2d matrix using word2vec, and then analyze the matrix to find different "features". Some features will be pre-made, others user-defined. 

Features are saved like this

```
app/features/featureName
  /ui
    /ui.json {
      name:"Kritiks (Neg)",
      publishedBy: "me",
      OutputSliders:{
        visualRange:[0,1],
        0:"hate K's",
        1:"love K's"
      },
      description:{
        short:"Can you run a K on AFF?",
        long: "This feature lets you filter judges based off of thier [...]"
      },
      icons:{
        (tbd)
      }
    }
    
  /trainingData
    /John Doe.txt
      Hi, I'm john doe. <k+>I love kritiks</k+>. Bye!
    /Jane Eyre.txt
      Jane Eyre. Debated at UTD for 100 years. <k->kritiks are terrible</k->.  

  /neuralNetwork
    /W2V v4.hdf5

    /NNlayers.json [
      {type:"dense",neurons:"100",activation:"relu"},
      {type:"dense",neurons:"100",activation:"relu"},
      {type:"dense",neurons:"1",activation:"relu"}
    ]

    /NNtraining.json {
      loss:"categoricalCrossentropy",
      optimizer:"adam"
    }
```

