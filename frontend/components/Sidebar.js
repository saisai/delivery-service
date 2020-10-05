import React, {useState, useEffect} from 'react';
import Link from "next/link";


function Sidebar() {
  const [permission, setPermission] = useState('')
  const [username, setUsername] = useState('')

  useEffect(() => {
    const permissions = localStorage.getItem('permissions')
    setUsername(localStorage.getItem('user'));
    setPermission(permissions);
  }, [])


  return (
    <div id="sidebar" className="sidebar">

      <div data-scrollbar="true" data-height="100%">

        <ul className="nav">
          <li className="nav-profile">
            <a data-toggle="nav-profile">
              <div className="cover with-shadow"/>
              <div className="image">
                <img src="/images/user/user-13.jpg" alt=""/>
              </div>
              <div className="info">
                <b className="caret pull-right"/>{username}
                <small>Stuff</small>
              </div>
            </a>
          </li>
        </ul>
        {permission === 'CAN_VIEW_OPERATOR_TAB' &&
        <ul className="nav">
          <li className="nav-header">Navigation</li>
          <li className="has-sub active">
            <a><Link href={"/dashboards/operator"}><span>Operator Dashboard</span></Link></a>
          </li>
          <li className="has-sub active" >
            <a><Link href={"/courier"}><span>courier track</span></Link></a>
          </li>
        </ul>
        }
        {permission === 'CAN_VIEW_CASHIER_TAB' &&
        <ul className="nav">
          <li className="nav-header">Navigation</li>
          <li className="has-sub active">
            <a>
              <b className="caret"/>
              <i className="fa fa-th-large"/>
              <Link href={"/dashboards/cashier"}><span>Cashier Dashboard</span></Link>
            </a>
          </li>
        </ul>
        }
      </div>
    </div>
  )
}

export default Sidebar