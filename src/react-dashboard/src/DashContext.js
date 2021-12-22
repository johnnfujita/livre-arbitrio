import React, { createContext, useContext, useEffect } from 'react'

const Dash = createContext();

const DashContext = ({ children }) => {
    const [currency, setCurrency] = React.useState('USD');
    const [symbol, setSymbol] = React.useState('$');

    useEffect(() => {
        if (currency === "USD")
            setSymbol('$');
        else if (currency === "BRL") setSymbol('R$');
    }, [currency]);
    return (
        <Dash.Provider value={{ currency, symbol, setCurrency }}>
            {children}
        </Dash.Provider>
    )
}

export default DashContext;

export const DashState = () => {
    return useContext(Dash);
}
