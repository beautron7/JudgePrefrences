## notes for word2vec
* regularize the middle layer so the weights are not insane
* maybye divide all of the Y values by x freqency to regularize it?

#### word2vec

Important link: http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/

1. Get a list of the top n=10,000 (?) ish words used in the wiki
    * half would be based off of how many wikis contain the word
    * half would be based off of how many times that word is mentioned across all wikis


2. Find every occourence of these words across all wikis


3. At each occourence, note the next w=2 words and the previous w words.
    * For example, the input
    ```
    the quick brown fox jumps over the lazy dog
    `               ^^^
    ```
    becomes
    `[(fox,quick),(fox,brown),(fox,jumps),(fox,over)]`


4. Train a neural network:
    1. Scheme:
        *  The networked is trained to take in the "selected word", or the first item of the tuple, and spit out the surrounding words.
        ```
        input: n input neurons          //each example lights up it's own input
          ...
        hidden: (f=300 neurons???)
          ...
        output: n output neurons        //what likley precedes &| follows this word?
        ```

    2. Explanation:
        * Whenever a word is put in, the network will spit out words that frequently surround it. This means if two different words are used in identical contexts, they will fire the same outputs.
        * For example, if the network was trained with `the quick WHITE fox` vs `the quick GRAY fox`, the words "white" and "gray" would trigger similar neural activity.
        * Thus, the network can be used to create a vector representation of those words. But instead of using the output layer, people look at the first hidden layer because a 300 dimensional vector is easier to manage than a 10,000 dimensional vector. So once the network is trained, we throw away the output layer
        * For most projects, google has it's own dataset that it trained with a ton of books, but I'm not using that becasue I need it to understand buzzwords.

#### Training data
I need to go in and label all of the judges philosophies

#### network ideas
* maybye it could be an "image" of 300px by (number of words)px
    * each word would be made into a 300px high collum by running it thru word2vec
    * turn a series of words into a sieries of 300px high collums, making an image
    * NN will then will scroll thru the entire philosophy (like a sidescroller) with a 300px by 30px "window", and evaluate wheither a series of words stands out as defining a charachteristic.
    * The inputs could be "vingetted" (the first layer would reduce the activations of the first and last words) so the neural network would automatically focus on the center.
    * could be trained with cherry-picked sentences like "i like k's" or similar stuff, because it would look at every sentence
