import Layout from "../../components/layout";
import React, {useState} from 'react';
import {loginPost, whoAmI} from "../../lib/login";
import LoginComponent from "../../components/login";



export default function Login() {


  return (
    <>
      <LoginComponent />
    </>
  )
}