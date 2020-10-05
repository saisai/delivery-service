import React, {useState, useEffect} from 'react';
import Sidebar from "./Sidebar";
import Main from "./main";
import Header from "./header";


function Layout({children}) {
  useEffect(() => {
    if (!localStorage.getItem('token')) {
      window.location.href = '/auth/login'
    }
  })

  return (
    <div id='page-container' className='page-sidebar-fixed page-header-fixed'>
      <Header />
      <div className={'sidebar'}/>
      <Sidebar/>
      <Main>
        <div className="content" id='content'>
          {children}
        </div>
      </Main>
    </div>
  )
}

export default Layout