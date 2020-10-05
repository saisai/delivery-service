import React, {useState} from "react";
import {fetchAddressFromServer} from "../../../lib/data_fetch";
import InputField from "../../input-number";
import SelectComponent from "../../select_component";


export default function Step1(props) {
  const [city, setCity] = useState(1);
  const [district, setDistrict] = useState(null)
  const [street, setStreet] = useState(null)
  const [districtDefault, setDistrictOption] = useState(null)
  const [streetDefault, setStreetOption] = useState(null)
  const [foundAddresses, setFoundAddresses] = useState([])
  const [house, setHouse] = useState('')
  const [flat, setFlat] = useState('')
  const [addressFrom, setAddressFrom] = useState({})
  const [userName, setUserName] = useState('')
  const [userPhone, setUserPhone] = useState('')
  const [floor, setFloor] = useState('')
  const [ransomSum, setRansomSum] = useState(0)

  const floorChange = (e) => {
    let floor = e.target.value;
    setFloor(floor);
    saveAddressFrom({floor: floor});
  }


  const changeOrderUser = (e) => {
    let userName = e.target.value;
    setUserName(userName);
    saveAddressFrom({user_name: userName});
  }

  const changeUserPhone = (e) => {
    let userPhone = e.target.value;
    setUserPhone(userPhone);
    saveAddressFrom({phoneNumber: userPhone});
  }

  const houseChange = (e) => {
    let houseNumber = e.target.value;
    setHouse(houseNumber);
    saveAddressFrom({house: houseNumber})
  }

  const flatChange = (e) => {
    let flatNumber = e.target.value;
    setFlat(flatNumber);
    saveAddressFrom({flat: flatNumber});
  }

  const saveAddressFrom = (updateItem) => {
    let address = {
      ...addressFrom,
      ...updateItem,
    }
    setAddressFrom(address);
    props.changeAddressFrom(address);
  }

  const streetsOptions = props.streets.map((street) => {
    return {value: street.id, label: street.name}
  })

  const districtOptions = props.districts.map((district) => {
    return {value: district.id, label: district.name}
  })

  const changeDistrict = (districtId) => {
    setDistrict(districtId);
    saveAddressFrom({district: districtId});
  }

  const changeStreet = (streetId) => {
    setStreet(streetId)
    saveAddressFrom({street:streetId})
  }

  const fetchAddress = (e) => {
    if (e.target.value.length > 0) {
      fetchAddressFromServer(e.target.value).then((data) => {
        setFoundAddresses(data)
      })
    } else {
      setFoundAddresses({})
    }
  }

  const selectAddress = (addr) => {
    let streetOption = {value: addr.street.id, label: addr.street.name};
    let districtOption = {value: addr.district.id, label: addr.district.name};
    setStreetOption(streetOption);
    setDistrictOption(districtOption);
    setHouse(addr.house);
    setFlat(addr.flat);
    saveAddressFrom({
      district: addr.district.id,
      street: addr.street.id,
      house: addr.house,
      flat: addr.flat
    });
    document.getElementById('found-address').value = '';
    setFoundAddresses({});
  }

  const changeRansomSum = (e) => {
    let ransomSum = e.target.value;
    setRansomSum(ransomSum);
    saveAddressFrom({ransom_sum: ransomSum});
  }

  return (
    <div className='col-xl-4 col-lg-6 ui-sortable'>
        <div className="panel panel-inverse">
          <div className='panel-heading ui-sortable-handle'>
            <h4 className="panel-title">Введите адрес отправки</h4>
          </div>
          <div className='panel-body bg-light'>
            <div className='slimScrollDiv' style={{position: "relative", overflow: "hidden", width: "auto"}}>
              <InputField
                fieldName={"Имя клиента"}
                placeholder={'Имя клиента'}
                fieldType={'text'}
                name={'firstname'}
                required={true}
                id={'username'}
                handleChange={changeOrderUser}
              />

              <InputField
                handleChange={changeUserPhone}
                fieldName={"Номер телефона"}
                placeholder={'700-00-00-00'}
                fieldType={'number'}
                name={'number'}
                required={true}
                id={'phone-number'}
              />

              <InputField
                handleChange={fetchAddress}
                fieldName={"Адрес в базе"}
                placeholder={'Freshbox'}
                fieldType={'text'}
                name={'number'}
                id={'found-address'}
              />
              {!!foundAddresses.length > 0 &&
              <div className='dropdown-menu dropdown-menu-right show'>
                <div>
                  {foundAddresses.map((addr, index) =>
                    <div style={{display: "flex", justifyContent: 'center'}} key={index}>
                      <a className="dropdown-item" key={index} onClick={() => selectAddress(addr)}>
                        {addr.custom_name}
                        <small> &nbsp; Адресс: {addr.district.name} {addr.street.name} {addr.house ? addr.house : ''}</small>
                      </a>
                    </div>
                  )}
                </div>
              </div>
              }
            </div>

            <div className="form-group row m-b-10">
              <label className="col-lg-3 text-lg-right col-form-label"><strong>Район</strong><span
                className="text-danger">*</span></label>
              <SelectComponent
                options={districtOptions}
                changeFunction={changeDistrict}
                placeHolder={'Район'}
                defaultInputValue={districtDefault}
              />
            </div>

            <div className="form-group row m-b-10">
              <label className="col-lg-3 text-lg-right col-form-label"><strong>Улица</strong><span
                className="text-danger">*</span></label>
              <SelectComponent
                options={streetsOptions}
                changeFunction={changeStreet}
                placeHolder={'Улица'}
                defaultInputValue={streetDefault}
              />
            </div>

            <div >

              <div>
                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Номер дома </label>
                  <div className="">
                    <input type="text" name="house" placeholder="" className="form-control" value={house}
                           onChange={houseChange}/>
                  </div>
                </div>

                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Номер квартиры </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" onChange={flatChange} value={flat}
                           className="form-control"/>
                  </div>
                </div>
              </div>

              <div>
                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Этаж </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" onChange={floorChange} value={floor}
                           className="form-control"/>
                  </div>
                </div>

                <div className="form-group row m-b-10">
                  <label className="col-lg-3 text-lg-right col-form-label">Домофон </label>
                  <div className="">
                    <input type="number" name="flat" placeholder="" className="form-control"/>
                  </div>
                </div>

                <div className="form-group row m-b-10">
                <label className="col-lg-3 text-lg-right col-form-label"><strong>Сумма выкупа</strong></label>
                <div className="col-lg-2 col-xl-2">
                  <input type="number" name="ransomSum" onChange={changeRansomSum} value={ransomSum} className="form-control"/>
                </div>
              </div>
              </div>

            </div>


          </div>
        </div>
      </div>
  )
}