import Layout from "../components/layout";
import React, {useEffect} from "react";
import {redirectToAppropriateDashboard} from "../lib/utils"


export default function Home() {

  useEffect(() => {
    redirectToAppropriateDashboard();
  }, [])

  return (
    <Layout/>
  )
}