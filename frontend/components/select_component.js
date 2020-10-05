import React, {useEffect, useState} from "react";
import Select from "react-select";

export default function SelectComponent({options, changeFunction, placeHolder, defaultInputValue, handleCreate}) {
  const [selectedOption, setSelectedOption] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  function handleChange(option) {
    setSelectedOption(option);
    changeFunction(option.value);
  }

  useEffect(() => {
    setSelectedOption(defaultInputValue);
    if(defaultInputValue) {
      changeFunction(defaultInputValue.value);
    }
  }, [defaultInputValue])

  return (
    <>
      <Select
        isClearable
        isDisabled={isLoading}
        isLoading={isLoading}
        onChange={handleChange}
        onCreateOption={handleCreate}
        options={options}
        value={selectedOption}
        className={'modalSelect'}
      />
    </>
  )
}