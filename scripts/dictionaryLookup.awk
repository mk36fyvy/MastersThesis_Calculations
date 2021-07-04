# Used to get the top enzymes with names in a list output
# Takes a dict-file ("key value" lines) and fills in the values for the keys in a second file. The keys must match with a space in front
# Usage: awk -f dictionaryLookup.awk dict.txt toFill.txt

NR == FNR { # perform this command only for the first given file
  sort -r
  k = " "$1
  rep[k] = "\t"$2
  next
}

{
  PROCINFO["sorted_in"] = "@ind_str_desc"
  for(key in rep){
    gsub(key, rep[key])
  }
  print
}
