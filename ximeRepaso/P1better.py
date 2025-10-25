xs = ['canvas', 'acquisitions', 'targets', 'urge', 'refer', 'occasion',
         'montana', 'hebrew', 'lightweight', 'were', 'respondent', 'hoped',
         'micro', 'forge', 'investigator', 'additional', 'symbol', 'prove',
         'holiday', 'competent', 'george', 'ability', 'upskirt', 'precision',
         'cow', 'photograph', 'chairman', 'electronic', 'float', 'spend',
         'starring', 'establishing', 'fold', 'logical', 'lower', 'ic',
         'boundaries', 'petersburg', 'grand', 'journalism', 'heard', 'chips',
         'global', 'pays', 'september', 'semiconductor', 'furnished',
         'wonderful', 'aged', 'generic', "as"]

max_len = max(len(word) for word in xs)
min_len = min(len(word) for word in xs)
largest_words = [word for word in xs if len(word) == max_len]
smallest_words = [word for word in xs if len(word) == min_len]
print(largest_words)
print(smallest_words)
