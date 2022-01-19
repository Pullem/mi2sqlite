# mi2sqlite
MediaInfo to SQLite ( all categories, all elements)

Here i try to store 'all' elements from MediaInfo in a sqlite database

in the root of the script we have three directories

  - media: our media storage, sometimes with non-media files (pdf, txt, ...) we filter with the help of an 'extensions' list
  - log: log files from MediaInfo, not necessary, just to compare with the content of sqlite
   - db: here the script saves the database(s)
      - every media file has an own database
      - inside this db every category ( General, Audio, Video, ...) has its own 'table'
      - a table has only two columns: 'MI_Element' and 'MI_Value', filled with 'all' and 'everything' which MediaInfo 'spits'

please consider, it's only my 'fun project'
