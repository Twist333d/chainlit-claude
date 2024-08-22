New features:
1. Add ability to upload files (vision)
2. Add ability to crawl, vectorize and retrieve information about documentation.
   - Select documentation
   - Crawl and get the results
   - Store in a local database
   - Setup RAG to answer questions with references


Improvements:
1. Improve search function:
   - Fix errors when parsing LinkedIn
   - Review & re-try, if necessary.
     - There has to be a review & re-try step before sending the results to the user.

UI:

Backend-only:
1. Proper logger integrated with the system

Issues:
- Performance metrics are not calculated correctly. They should follow each API response, however, after 
  introduction of a tool use they do not.
- 

