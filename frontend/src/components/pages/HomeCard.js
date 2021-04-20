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
import { primaryTheme } from "./../../utils/constants";
import {
  ArgumentAxis,
  ValueAxis,
  Chart,
  LineSeries,
} from "@devexpress/dx-react-chart-material-ui";

function HomeCard(props) {
  return (
     <div>
        <Card variant="outlined" className="home-info-card card">
            <img className="home-image" src={homeImg} />
            <Box className="home-info-text">
              <Typography className="home-address" variant="h6">
                {props.address}
              </Typography>
              <Typography variant="body">
                Bedrooms: {props.bedrooms}
                <br />
                Bathrooms: {props.bathrooms}
                <br />
                Sqft.: {props.squareFeet}
              </Typography>
            </Box>
          </Card>
     </div>
  );
}
export default HomeCard;
