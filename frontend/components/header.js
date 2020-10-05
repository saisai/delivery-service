import {useEffect, useState} from "react";


export default function Header() {
  const [showMenu, setShowMenu] = useState(false);

  function menuHandlerClick(e) {
    e.preventDefault();
    setShowMenu(!showMenu);
  }

  function logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('permissions')
    window.location.href = '/auth/login'
  }
  let userName = '';

  useEffect(() => {
    userName = localStorage.getItem('user')
  }, [])

  const styles = {
    "position": "absolute",
    "willChange": "transform",
    "top": "0px",
    "left": "0px",
    "transform": "translate3d(4px, 50px, 0px)"
  }


  return (
    <>
      <div id="header" className="header navbar-default">
        <div className="navbar-header">
          <a className="navbar-brand">
            <span className="navbar-logo"/> <b>Colibri</b> Admin
          </a>
          <button type="button" className="navbar-toggle" data-click="sidebar-toggled">
            <span className="icon-bar"/>
            <span className="icon-bar"/>
            <span className="icon-bar"/>
          </button>
        </div>
        <ul className="navbar-nav navbar-right">
          <li className="dropdown navbar-user">
            <a href="#" className="dropdown-toggle" data-toggle="dropdown" onClick={menuHandlerClick}>
              <img src="/images/user/user-13.jpg" alt=""/>
              <span className="d-none d-md-inline">{userName}</span> <b className="caret"/>
            </a>
            { showMenu &&
            <div className="dropdown-menu dropdown-menu-right show"
                 style={styles}
                 x-placement="bottom-end">
              <a className="dropdown-item">Edit Profile</a>
              <a className="dropdown-item"><span
                className="badge badge-danger pull-right">2</span> Inbox</a>
              <div className="dropdown-divider"/>
              <a className="dropdown-item" onClick={logout}>Log Out</a>
            </div>
            }
          </li>
        </ul>
      </div>
    </>
  )
}