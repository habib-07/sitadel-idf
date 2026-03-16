
ui <- dashboardPage(
  skin = "blue",
  dashboardHeader(title = "SITADEL Ile-de-France"),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Vue d ensemble",  tabName="overview", icon=icon("chart-bar")),
      menuItem("Types logement",  tabName="types",    icon=icon("building")),
      menuItem("Par departement", tabName="dept",     icon=icon("map-marker")),
      menuItem("Carte communale", tabName="carte",    icon=icon("map"))
    ),
    hr(),
    sliderInput("filtre_annee", "Periode",
      min=2011, max=2024, value=c(2011,2024), step=1, sep=""),
    pickerInput("filtre_dept", "Departements",
      choices=c("75","77","78","91","92","93","94","95"),
      selected=c("75","77","78","91","92","93","94","95"),
      multiple=TRUE, options=list(`actions-box`=TRUE))
  ),
  dashboardBody(
    tabItems(

      tabItem("overview",
        fluidRow(
          valueBoxOutput("vbox_aut",  width=3),
          valueBoxOutput("vbox_com",  width=3),
          valueBoxOutput("vbox_ratio",width=3),
          valueBoxOutput("vbox_evol", width=3)
        ),
        fluidRow(
          box(title="Autorisations vs mises en chantier IDF", width=8,
              plotOutput("p_aut_com", height=320)),
          box(title="Repartition par type (2024)", width=4,
              plotOutput("p_type_pie", height=320))
        )
      ),

      tabItem("types",
        fluidRow(
          box(title="Evolution par type de logement", width=12,
              plotOutput("p_types_evol", height=350))
        ),
        fluidRow(
          box(title="Part des types par annee (%)", width=12,
              plotOutput("p_types_part", height=300))
        )
      ),

      tabItem("dept",
        fluidRow(
          box(title="Autorisations par departement", width=6,
              plotOutput("p_dept_aut", height=380)),
          box(title="Mises en chantier par departement", width=6,
              plotOutput("p_dept_com", height=380))
        )
      ),

      tabItem("carte",
        fluidRow(
          box(width=12,
            radioGroupButtons("carte_var", "Variable a cartographier",
              choices=c("Autorisations"="log_aut","Mises en chantier"="log_com"),
              selected="log_aut", status="primary"),
            pickerInput("carte_annee", "Annee", 
              choices=2011:2024, selected=2023, multiple=FALSE),
            leafletOutput("carte_com", height="520px")
          )
        )
      )
    )
  )
)

