import './App.css';
import { Route, Routes } from 'react-router-dom';
import { Homepage, SymbolDetail } from './Pages';
import { Header } from './Components/';
import { makeStyles, createTheme, ThemeProvider } from '@material-ui/core/styles';
import DashContext from './DashContext';
import 'react-alice-carousel/lib/alice-carousel.css';

function App() {
  const darkTheme = createTheme({
    palette: {
      primary: {
        main: '#212121',
      },
      type: 'dark'
    }
  })

  const useStyles = makeStyles(theme => ({
    App: {
      backgroundColor: "#14161a",
      color: "white",
      minHeight: "100vh",
    }
  }));
  const classes = useStyles();


  return (
    <DashContext>

      <ThemeProvider theme={darkTheme}>
        <div className={classes.App}>
          <Header />
          <Routes>
            <Route exact path="/" element={<Homepage />} />
            <Route exact path="/symbols/:symbol" element={<SymbolDetail />} />
          </Routes>

        </div >
      </ThemeProvider>
    </DashContext>
  );
}

export default App;
