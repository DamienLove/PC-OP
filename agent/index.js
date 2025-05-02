import "dotenv/config";
import { initializeApp, cert } from "firebase-admin/app";
import { getFirestore, Timestamp } from "firebase-admin/firestore";
import { execSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import express from "express";

initializeApp({ credential: cert(path.resolve(process.env.GOOGLE_APPLICATION_CREDENTIALS)) });
const db = getFirestore();
const COL = process.env.COMMANDS_COLLECTION || "commands";

console.log("[agent] connected. Listening for commands…");

db.collection(COL).where("status","==","new").onSnapshot(snap=>{
  snap.docChanges().forEach(c=>c.type==="added"&&handle(c.doc));
});

async function handle(doc){
  const {action,payload}=doc.data();
  console.log("[NEW]",doc.id,action);
  try{
    let output="";
    if(action==="shell") output=execSync(payload.cmd,{encoding:"utf8"});
    else if(action==="ahk"){
      const p=`tmp-${doc.id}.ahk`;
      fs.writeFileSync(p,payload.script);
      output=execSync(`AutoHotkey64.exe "${p}"`,{encoding:"utf8"});
      fs.unlinkSync(p);
    } else throw new Error("unknown action");
    await doc.ref.update({status:"done",output,finishedAt:Timestamp.now()});
    console.log("[OK ]",doc.id);
  }catch(err){
    await doc.ref.update({status:"error",error:err.message,finishedAt:Timestamp.now()});
    console.error("[ERR]",doc.id,err.message);
  }
}

const app=express();
app.get("/hello",(_,r)=>r.send("OK"));
app.listen(4040,()=>console.log("[agent] health endpoint on 4040"));
{
  "functions": {
    "source": "functions",
    "runtime": "nodejs20"
  }
}
