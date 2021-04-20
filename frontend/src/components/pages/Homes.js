import React from "react";
import {
  Box,
  Card,
  Typography,
  Button,
  requirePropFactory,
  FormLabel,
  FormControl,
  FormGroup,
  FormControlLabel,
  Checkbox,
  ThemeProvider,
} from "@material-ui/core";
import "./../../global.css";
import "./Home.css";
import homeImg from "./../../resources/images/home.jpeg";
import HomeCard from "../../components/pages/HomeCard";
import { primaryTheme } from "./../../utils/constants";
import SearchBar from 'material-ui-search-bar';
import {
  ArgumentAxis,
  ValueAxis,
  Chart,
  LineSeries,
} from "@devexpress/dx-react-chart-material-ui";

const mockProps = {
    homeData: [{
      address: "25681 Estoril Street, Valencia CA 91355",
      bedrooms: 4,
      bathrooms: 2,
      squareFeet: 3000,
      imgSrc: homeImg,
    },
    {
        address: "25681 Estoril Street, Valencia CA 91355",
        bedrooms: 4,
        bathrooms: 2,
        squareFeet: 3000,
        imgSrc: homeImg,
     }],
  };

function Homes(props) {
    props = mockProps;
  return (
     <div>
        <SearchBar
            onChange={() => console.log('onChange')}
            onRequestSearch={() => console.log('onRequestSearch')}
            style={{
              margin: '0 auto',
              maxWidth: 800
            }}
        />
        {props.homeData.map((data)=> {return (<HomeCard{...data}/>)})};
     </div>
  );
}
export default Homes;
