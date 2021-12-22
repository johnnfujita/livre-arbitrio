import React from 'react'
import { Container, makeStyles, Typography } from '@material-ui/core'
import Caroussel from './Caroussel';


const useStyles = makeStyles(theme => ({
    banner: {
        backgroundImage: "url(./banner.jpg)"
    },
    bannerContent: {
        height: 400,
        display: "flex",
        flexDirection: "column",
        paddingTop: 25,
        justifyContent: "space-around"
    },
    tagline: {
        display: "flex",
        height: "40%",
        flexDirection: "column",
        center: "center",
        justifyContent: "center",
        textAlign: "center"
    }
}));

const Banner = () => {

    const classes = useStyles();
    return (
        <div className={classes.banner}>
            <Container className={classes.bannerContent}>
                <div className={classes.tagline}>
                    <Typography
                        variant="h2"
                        style={{
                            fontWeight: "bold",
                            marginBottom: 15,
                            fontFamily: "Roboto",
                        }}
                    >
                        MoneyMaker Dashboard
                    </Typography>
                    <Typography
                        variant="subtitle1"
                        style={{
                            color: "darkgrey",
                            textTransform: "capitalize",
                            fontFamily: "Roboto",
                        }}
                    >
                        Seek Arbitrage Opportunities
                    </Typography>
                </div>
                <Caroussel />
            </Container>
        </div>
    )
}

export default Banner
