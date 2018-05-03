# What is this?
this is a bunch of disconnected thoughs about the program

# What does the end program look like?
When the end user starts the program, they can:
1. type in their numerical preferences and click a button to get a pref sheet
2. select a few attributes and have the program  "highlight" sentences that are indicative of that attribute.
3. rate a couple of paradigms so that the network can learn what the user likes and take over

# What do you mean neumerical prefrences?
*Kevin can you reword this?*
Picking a judge involves weighing many factors;
One has to consider things such as Experience, Age, Prefrences on Kritiks, etc. when considering a judge.
But every team has different needs and desires; One team may want judges that like speed reading, while another may not. 
So instead of waiting for a NN to "guess" what you're looking for, the final program will be able to tell where a judge lies on a chart and  let you say "I want judges with experience",  team is looking for, the are looking for by example, you can tell it "show me judges who like speaking quickly." 



 The program should look at a judge and use various neural networks to "score" judges based off of these properties, so the user can just filter judges based off of thier numbers.


  so the end user can quickly filter out judges based off of certain peramters.
The program should be able to read through a paradigm and 
Let's say you want experienced judges who like K's. The program should find  
 create a list of attributes It makes more sense to let someone boil down what they are looking for onto a chart, and then train a network to give neumeric information about a judge's personal beliefs

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

