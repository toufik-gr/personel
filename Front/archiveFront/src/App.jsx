import { useState, useEffect } from "react";
// import Header from "./components/Header";
import MainLayout from "./layouts/MainLayout";
import Home from "./pages/Home";
import UpdateEnsPage from "./pages/enseignant/UpdateEnsPage";
import AddEnseignantPage from "./pages/enseignant/AddEnseignantPage";
import EnseignantsPage from "./pages/enseignant/EnseignantsPage";
import AllOperations from "./pages/AllOperations";
import EmployesPage from "./pages/employes/EmployesPage";
import AddEmployePage from "./pages/employes/AddEmployePage";
import ContratPage from "./pages/contrat/ContratPage";
import AddContratPage from "./pages/contrat/AddContratPage";
import Login from "./pages/log-out/Login";
import Logout from "./pages/log-out/Logout";

import {
  Route,
  RouterProvider,
  createBrowserRouter,
  createRoutesFromElements,
} from "react-router-dom";
import TableEns from "./components/TableEns";
import axios from "axios";
import { toast } from "react-toastify";

function App() {
  const updateEns = (data, id) => {
    axios
      .put(`http://127.0.0.1:8000/enseign/ens/${id}/`, data)
      .then((res) => {
        console.log(res.data);
        toast.success("Enseignant updated succesfully");
      })

      .catch((err) => console.log(err.message));
  };

  const router = createBrowserRouter(
    createRoutesFromElements(
      <>
        {/* Routes without layout */}
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        {/*  */}
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Home />} />
          {/* Enseignant */}
          <Route path="/allEns" element={<EnseignantsPage />} />
          <Route path="/add-ens" element={<AddEnseignantPage />} />
          <Route
            path="/AllOperations/emp/:id"
            element={<AllOperations type="employe" />}
          />
          <Route
            path="/AllOperations/ens/:id"
            element={<AllOperations type="enseignant" />}
          />
          <Route
            path="/AllOperations/contrat/:id"
            element={<AllOperations type="contrat" />}
          />
          {/*<Route
            path="/update-ens/:id"
            element={<UpdateEnsPage updateEns={updateEns} />}
          />*/}
          {/* Employe */}
          <Route path="/allEmp" element={<EmployesPage />} />
          <Route path="/add-emp" element={<AddEmployePage />} />

          {/* Contrat */}
          <Route path="/allContrat" element={<ContratPage />} />
          <Route path="/add-contrat" element={<AddContratPage />} />
        </Route>
      </>
    )
  );

  return <RouterProvider router={router} />;
}
export default App;
