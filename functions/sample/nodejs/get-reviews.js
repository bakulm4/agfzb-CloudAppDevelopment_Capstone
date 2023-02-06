/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
 function main(params) {
     
     const IAM_API_KEY = 'VHPowScjpMEuMvqdJHGV7t2vyhoQP_sWukDkhlJ-OOga';
     const COUCH_URL = 'https://32b60b7a-3008-49d8-9c8a-e9c4703fd00f-bluemix.cloudantnosqldb.appdomain.cloud';
     const DB_NAME = 'reviews'
     
     const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY });
     
     const cloudant = CloudantV1.newInstance({
       authenticator: authenticator
     });
     cloudant.setServiceUrl(COUCH_URL);
     
     if(params.dealerId)
         return getMatchingRecords(cloudant,DB_NAME,{dealership:params.dealerId});
         
     return getAllRecords(cloudant,DB_NAME);
 }
 function getMatchingRecords(cloudant,dbname, selector) {
    return new Promise((resolve, reject) => {
        cloudant.postFind({db:dbname,selector:selector})
                .then((result)=>{
                 console.log(`Get Matching Records: `,result.result.docs);
                   let code = 200;
                   if (result.result.docs.length === 0) {
                       code = 404;
                   }
                  resolve({
                   statusCode: code,
                   headers: { 'Content-Type': 'application/json' },
                   result:result.result.docs});
                })
                .catch(err => {
                   console.log(err);
                    reject({
                       statusCode: 500,
                       err: `Something went wrong: ${err.message}` 
                     });
                });
         })
}

 function getAllRecords(cloudant,dbname) {
      return new Promise((resolve, reject) => {
          cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
              .then((result)=>{
                 console.log(`getAllRecords - result: `,result.result.rows);
                   let code = 200;
                   if (result.result.rows.length === 0) {
                       code = 404;
                   }
                resolve({
                    statusCode: code,
                    headers: { 'Content-Type': 'application/json' },
                    result:result.result.rows
                });
              })
              .catch(err => {
                 console.log(err);
                 reject({
                     statusCode: 500,
                     err: `Something went wrong: ${err.message}` 
                 });
              });
          })
  }
  
