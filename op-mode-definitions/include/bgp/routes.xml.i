<!-- included start from bgp/routes.xml.i -->
<leafNode name="routes">
  <properties>
    <help>Show routes learned from BGP neighbor</help>
  </properties>
  <command>${dozenos_op_scripts_dir}/vtysh_wrapper.sh $@</command>
</leafNode>
<!-- included end -->
