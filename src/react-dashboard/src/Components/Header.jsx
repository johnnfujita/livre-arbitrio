import React from 'react'
import { AppBar, Container, Select, Toolbar, Typography, MenuItem } from '@material-ui/core'
import { makeStyles } from '@material-ui/styles'
import { Link } from 'react-router-dom';
import { DashState } from '../DashContext';



const useStyles = makeStyles((theme) => ({
    title: {
        flex: 1,
        color: "aqua",
        fontFamily: "Roboto",
        fontWeight: "bold",
        cursor: "pointer"
    }
}))
const Header = () => {
    const classes = useStyles();
    const { currency, setCurrency } = DashState();
    console.log(currency)
    return (
        <AppBar color="transparent" position="static">
            <Container>
                <Toolbar>
                    <Typography variant="h6" className={classes.title}>
                        <Link to="/"> React Dashboard</Link>
                    </Typography>
                    <Select variant="outlined" style={{ width: 100, height: 40, marginRight: 15 }} value={currency} onChange={(e) => setCurrency(e.target.value)}>
                        <MenuItem value={"USD"}>
                            USD
                        </MenuItem>
                        <MenuItem value={"BRL"}>
                            BRL
                        </MenuItem>
                    </Select>
                </Toolbar>
            </Container>
        </AppBar>
    )
}

export default Header
