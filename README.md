This is a text summarization model.
</br>
This model is specifically designed for the lease summarization text and its a very enhance commercially based Model.
</br>
we load the pretined model facebook/bart-large-cnn which having a 340M parameters
</br>
In this model load the pdf file which heaving a lease document and its create a summary which heaving landload,Tenana names .There location, aggrement detail and time.
</br>
Here is a some output:
</br>
{
  "Parties_Detail_and_Address": [
    "The lease agreement was made and entered into this 10  aay of February 2000  by and between the two companies.",
    "The terms of the agreement are as follows  The lease is for a period of 10 years.",
    "LEASE AGREEMENT between JOSEPH SUPOR and DOMINATE FOOD SERVICES II L.L.C.  a New Jersey limited liability company with a principle of partnership.",
    "The terms of the lease are set out in Schedule \"A\" of this lease.",
    "The premises are to be used for the purposes of a Burger King.",
    "The lease is for a building to be erected at the same location.",
    "The building is located at Harrison Avenue and Supor Boulevard  Harrison  New Jersey.",
    "The landlord is called the \"Lessee\" The landlord has leased  rented  let and demised the premises."
  ],
  "Contract_Detail(Agreement)": "The guaranteed minimum annual rental shall be payable on the first day of each month during the term of the lease. The term of this lease shall commence (\"commencement date\") with a date 
  </br>
  being a date either thirty (30) days following the date of the issuance of a Certificate of Occupancy for said building. Restaurant (as hereinafter defined) shall include a restaurant (with a drive-thru window) franchised 
  </br>
  or owned by Burger King. Lessor agrees to construct a Burger King Restaurant and related site improvements on the demised premises. The first monthly installment shall be paid upon execution of the Lease. The minimum
  </br>
  rental will be $80 00000 per year during years 1-20  $6 66667 per month."
  </br>
}
</br>
Download the model and gives path to the lease documents and visualize the funcionality
