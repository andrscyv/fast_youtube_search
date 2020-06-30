# Fast Youtube Search

This is a simple library that allows you to search videos on Youtube.

It is fast because it doesn't use selenium.

For each video it returns the name, id , and the thumbnail's url.
# Install 
```bash
pip install fast-youtube-search
```
# Usage

```python
 from fast_youtube_search import search_youtube

 results = search_youtube(['jorja', 'smith']) # receives an array of search terms as argument

 print(results) #returns a list of results(dictionaries)

 print(results[0]) # a dictionary with properties name, id and img
# OUTPUT 
# {
#  'name': 'Jorja Smith - Blue Lights | A COLORS SHOW', 
#  'id': 'fYwRsJAPfec', 
#  'img': 'https://i.ytimg.com/vi/fYwRsJAPfec/hqdefault.jpg'
#  }

#Optional arguments
# max_num_results : max number of results that the function returns
results = search_youtube(['jorja', 'smith'], max_num_results = 2)
```