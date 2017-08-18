import nltk

class Analyzer():
    """Implements sentiment analysis."""
    
    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        # declare a set for negatives and positives
        self.pos_text = set()
        self.neg_text = set()
        
        # attach tokenizer on init
        self.tokenizer = nltk.tokenize.TweetTokenizer()
        
        with open(positives) as pos_file:
            for row in pos_file:
                # if it doesn't start with ;, add it to your positive set
                if (row.startswith(";") is False):
                    self.pos_text.add(row.rstrip("\n"))
        pos_file.close()
        
        with open(negatives) as neg_file:
            for row in neg_file:
                # if it doesn't start with ;, add it to your positive set
                if (row.startswith(";") is False):
                    self.neg_text.add(row.rstrip("\n"))
        neg_file.close()

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        
        # get your tokens
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = self.tokenizer.tokenize(text)
        
        # go through full text passed and calculate score
        score = 0
        for token in tokens:
            lwrToken = token.lower()
            if lwrToken in self.pos_text:
                score += 1
            elif lwrToken in self.neg_text:
                score -= 1
        
        return score
