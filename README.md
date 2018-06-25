# pan-route-kill
A very basic python script to generate thousand of static route in your Palo Alto Networks equipement.
Usefull to perform Dynamic routing test like exporting a big number of route in BGP / OSPF.
I originally needed it to get a better understanding of route manipulation and routing policies.

- Change the following variable in the script 
  - ip
  - username
  - password
- Execute the script
- Commit in PanOS ( the script only alter the candidate configuration )
