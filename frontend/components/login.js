import React, {useState, useEffect} from "react";
import {loginPost, whoAmI} from "../lib/login";
import { useRouter } from 'next/router';
import {redirectToAppropriateDashboard} from "../lib/utils";


function login(userName, password) {
  let userData = {}
  loginPost(userName, password).then(data => {
    userData = data
    const {first_name, id, token} = userData
    if (token) {
      localStorage.setItem('user', first_name)
      localStorage.setItem('user_id', id)
      localStorage.setItem('token', token)
      whoAmI().then(data_info => {
        let {permissions} = data_info;
        localStorage.setItem('permissions', permissions)
        redirectToAppropriateDashboard()
      })
    }
  })
}

export default function Login() {
  const [password, setPassword] = useState('');
  const [userName, setuserName] = useState('');
  const router = useRouter()

  function changePassword(e) {
    setPassword(e.target.value)
  }

  function changeUserName(e) {
    setuserName(e.target.value)
  }

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (token) {
      router.push('/')
    }
  }, [])

  return (
    <>
      <div className="login-cover">
        <div className="login-cover-image" data-id="login-cover-image"/>
        <div className="login-cover-bg">
        </div>
      </div>
      <div className="login login-v2 animated fadeIn" data-pageload-addclass="animated fadeIn">
        <div className="login-header">
          <div className="brand">
            <span className="logo"/> <b>Colibri</b> Admin
            <small>Только для персонала</small>
          </div>
          <div className="icon">
            <i className="fa fa-lock"/>
          </div>
        </div>

        <div className="login-content">
          <div className="form-group m-b-20">
            <input type="text" className="form-control form-control-lg" placeholder="имя пользователя"
                   required="" onChange={changeUserName}/>
          </div>
          <div className="form-group m-b-20">
            <input type="password" className="form-control form-control-lg" placeholder="Пароль"
                   required="" onChange={changePassword}/>
          </div>
          <div className="checkbox checkbox-css m-b-20">
            <input type="checkbox" id="remember_checkbox"/>
            <label htmlFor="remember_checkbox">
              Запомнить
            </label>
          </div>
          <div className="login-buttons">
            <button className="btn btn-success btn-block btn-lg" onClick={login.bind(null, userName, password)}>Войти
            </button>
          </div>
        </div>
      </div>
    </>
  )
}